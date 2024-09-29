class MessagesController < ApplicationController
  def create
    room = if room_id.nil?
                CreateDefaultRoom.call(current_user)
              else
                Room.find(room_id)
              end

    @message = Message.create!(user: current_user, text: , room_id: room.id, llm: params[:llm])

    if @message.text.downcase.match?(/позови человека/) || @message.text.downcase.match?( /оператор/)
      room.update(human_need: true)
    else
      if room.kind.main? && !current_user.admin?
        @assistant_message = Message.create!(user: current_user, text: , room_id: room.assistant_room_id, llm: 'enabled')
      end
      LlmJob.perform_later(@message)
      LlmJob.perform_later(@assistant_message)
    end

  end
  def index
    @messages = Message.where(room_id: )

    if params[:search].present?
      search_term = "%#{params[:search]}%"
      @messages = @messages.where('text LIKE ?', search_term)
    end

    @messages = @messages.order(created_at: :desc).offset(offset).limit(limit)
  end


  private
  def text
    params.require(:text)
  end
  def room_id
    params[:room_id]
  end


  def offset
    params[:offset] || 0
  end

  def limit
    params[:limit] || 20
  end

end