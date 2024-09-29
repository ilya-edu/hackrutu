class PredictController < ApplicationController
  def predict
    articles = SemanticSearch.new.perform(params[:question], :chunks)[0..3].map(&:article)
    articles = articles.reject{ _1.name.match? /Условия размещения контента|ГЕНЕРАЛЬНОЕ ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ RUTUBE/}
    article = most_frequent_or_first(articles)
    room = Room.find_or_create_by(name: "Комната для тестового апи")
    message = Message.new(text: params[:question], user: User.tester, room_id: room.id, llm: 'enabled')
    message.skip_message_create_job
    message.save!
    new_message = LlmJob.new.perform(message)
    render json: { answer: new_message.text, class_1: article.category1.strip, class_2: article.category2.strip }
  end
  def most_frequent_or_first(articles)
    frequency = Hash.new(0)
    articles.each { |article| frequency[article] += 1 }
    most_frequent_article = frequency.max_by { |_, count| count }[0]
    if frequency.values.uniq.length == frequency.size
      articles.first
    else
      most_frequent_article
    end
  end
end