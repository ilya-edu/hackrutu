class AddVersionChange < ActiveRecord::Migration[7.1]
  def change
    drop_table :versions
  end
end
