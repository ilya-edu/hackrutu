class AddLastMessageToMessage < ActiveRecord::Migration[7.1]
  def change
    add_column :messages, :last_message, :boolean
  end
end
