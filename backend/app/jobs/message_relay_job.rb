class MessageRelayJob < ApplicationJob
  queue_with_priority 5
  queue_as :relays

  def perform(message)
    puts "Relaying message #{message.id}"
    payload =  {kind: "new_message", object: render_message(message)}
    ActionCable.server.broadcast "room_and_messages#{message.room.creator_id}", payload
    ActionCable.server.broadcast "room_and_messages_admin", payload
  end
  private

  def render_message(message)
    JSON.parse! ApplicationController.renderer.render(partial: 'messages/message', locals: { message: message })
  end
end