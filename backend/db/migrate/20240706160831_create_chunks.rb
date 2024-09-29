class CreateChunks < ActiveRecord::Migration[7.1]
  def change
    create_table :chunks do |t|
      t.belongs_to :article
      t.text :content
      t.vector "embedding", limit: 1024
      t.string "search_index"
      t.timestamps
    end
  end
end
