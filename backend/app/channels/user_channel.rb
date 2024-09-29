class UserChannel < ApplicationCable::Channel
  def subscribed
    stop_all_streams
    if current_user.admin?
      stream_from "room_and_messages_admin"
    else
      stream_from "room_and_messages#{current_user.id}"
    end
  end

  def unsubscribed
    stop_all_streams
  end

  def fetch_room
    room = Room.main.find_by(creator_id: current_user.id)
    if room.nil?
      room = CreateDefaultRoom.call(current_user)
    end

    ActionCable.server.broadcast "room_and_messages#{current_user.id}", {kind: 'room_id', room_id: room.id, assistant_room_id: room.assistant_room_id}
  end
end
