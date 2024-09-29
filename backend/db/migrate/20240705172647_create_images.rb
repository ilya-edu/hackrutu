class CreateImages < ActiveRecord::Migration[7.1]
  def change
    create_table :images do |t|
      t.string :link
      t.text :content
      t.references :article
      t.vector "embedding", limit: 1024
      t.string "search_index"
      t.timestamps
    end
  end
end
