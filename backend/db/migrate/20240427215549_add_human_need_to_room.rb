class AddHumanNeedToRoom < ActiveRecord::Migration[7.1]
  def change
    add_column :rooms, :human_need, :boolean
  end
end
