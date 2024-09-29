class AddCreatorIdToRoom < ActiveRecord::Migration[7.1]
  def change
    add_column :rooms, :creator_id, :bigint
  end
end
