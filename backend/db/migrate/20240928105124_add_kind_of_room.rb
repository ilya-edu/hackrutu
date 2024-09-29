class AddKindOfRoom < ActiveRecord::Migration[7.1]
  def change
    add_column :messages, :llm, :string
    add_column :rooms, :kind, :string
    add_column :rooms, :main_room_id, :bigint
  end
end
