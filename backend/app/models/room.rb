class Room < ApplicationRecord
  extend Enumerize
  enumerize :kind, in: [:main, :assistant], scope: :shallow, default: :main
  has_many :messages, dependent: :destroy
  has_many :users, through: :messages
  belongs_to :creator, class_name: 'User', optional: true
  belongs_to :main_room, class_name: 'Room', optional: true
  has_one :assistant_room, class_name: 'Room', inverse_of: :main_room
  def name
    "Комната пользователя #{creator&.name}"
  end

  after_create_commit -> (room) {RoomRelayJob.perform_later(room)}
  def assistant_room_id
    assistant_room&.id
  end
end
