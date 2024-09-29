class RoomRelayJob < ApplicationJob
  queue_as :relays
  queue_with_priority 5

  def perform(room)
    payload = {kind: "new_room", object: render_room(room)}
    ActionCable.server.broadcast "room_and_messages_admin", payload
    ActionCable.server.broadcast "room_and_messages#{room.creator_id}", payload
  end
  private

  def render_room(room)
    JSON.parse! ApplicationController.renderer.render(partial: 'rooms/room', locals: { room: room })
  end
end