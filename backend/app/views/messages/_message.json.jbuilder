json.extract! message, :id, :room_id, :assistant_room_id,  :user_id, :text, :tg_text, :last_message, :references, :created_at, :updated_at
json.user do
  json.partial! message.user, partial: "users/user", as: :user
end