class CreateVersionGroups < ActiveRecord::Migration[7.1]
  def change
    create_table :version_groups do |t|
      t.timestamps
      t.string :name
    end
  end
end
