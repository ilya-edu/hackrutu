class CreateDefaultRoom
  def self.call(current_user, text = nil)
    text ||= "Комната пользователя #{current_user.name}"
    room = Room.create!(creator_id: current_user.id, name: text, kind: 'main')
    room.assistant_room = Room.create!(creator_id: current_user.id, name: text, kind: 'assistant')
    room
  end
end