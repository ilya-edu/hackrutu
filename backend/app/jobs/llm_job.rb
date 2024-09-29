class LlmJob < ApplicationJob
  queue_with_priority 2
  queue_as :llm_processing
  def perform(message)
    return if message.llm.disabled?
    chunks = SemanticSearch.new.perform(message.text, :chunks)[0..4]
    context = build_context(chunks)

    message.update(context: context )
    config = Config.first_or_create
    system_prompt = config.system
    user_prompt = config.user % { context:, query: message.text }
    prompt = "#{system_prompt} #{user_prompt}"
    puts 'Start LLM'
    Ollama.new(
      credentials: { address: config.llm_url  },
      options: { server_sent_events: true }
    ).chat(
      { model: config.llm,
        options: {
          temperature: config.temperature
        },
        messages: [
          { role: "system", content: system_prompt },
          { role: "user", content: user_prompt }
        ]
      },
      server_sent_events: true
    ) do |event, raw|
      puts event
      puts @message.inspect
      @message ||= Message.new(text: "" , room_id: message.room_id, user: User.find_or_create_by(name: "llm"), references: build_references(chunks), context: prompt  )
      @message.skip_message_create_job = true
      @message.save! unless @message.persisted?
      @message.update(text: "#{@message.text}#{event['message']['content']}", last_message: event['done'] )
      MessageRelayJob.new.perform(@message)
    end
    @message
  rescue StandardError => e
    puts e.backtrace
    Message.create(text: build_fallback_response(chunks) , room_id: message.room_id, user: User.find_or_create_by(name: "llm"), references: build_references(chunks), context: prompt  )
  end
  def build_context(chunks)

    chunks.map do |chunk|
      article = chunk.article
      <<-TEXT.strip_heredoc
#{chunk.search_index}
      TEXT
    end.join("\n\n\n-------------------------------------------------------------------------------------------------------\n\n\n")
  end

  def build_references(chunks)
    Article.where(id: chunks.map(&:article_id).uniq[0..5]).map do |article|
      url = article.link.start_with?("http") ? article.link : "https://rutube-copilot-api.kovalev.team/articles/#{article.link}"
      {
        name: article.name,
        url:
      }.to_json
    end
  end
  def build_fallback_response(chunks)
    chunks[0..5].map do |chunk|
      article = chunk.article
      next if article.nil?
      <<-TEXT.strip_heredoc
        1. [#{article.name}](https://rutube-copilot-api.kovalev.team/articles/#{article.link})
      TEXT
    end.compact.join("\n\n")
  end
end