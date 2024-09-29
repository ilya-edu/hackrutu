class ChangeType < ActiveRecord::Migration[7.1]
  def change
    change_column :messages, :context, :text
  end
end
