class CreateArticles < ActiveRecord::Migration[7.1]
  def change
    create_table :articles do |t|
      t.string :name
      t.text :content
      t.string :version
      t.string :link
      t.references :version_group
      t.vector "embedding", limit: 1024
      t.string "search_index"
      t.timestamps
    end
  end
end
