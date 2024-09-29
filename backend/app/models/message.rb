class Message < ApplicationRecord
  extend Enumerize
  enumerize :llm, in: [:enabled, :disabled], default: :enabled
  belongs_to :user
  belongs_to :room
  attr_accessor :skip_message_create_job
  after_create_commit -> (message) { MessageRelayJob.perform_later(message) }, unless: :skip_message_create_job

  def assistant_room_id
    room.assistant_room_id
  end
  def tg_text
    text[..4094]
  end
end
