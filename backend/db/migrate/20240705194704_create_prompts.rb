class CreatePrompts < ActiveRecord::Migration[7.1]
  def change
    create_table :prompts do |t|
      t.text :system, default: ''
      t.text :user, default: ''
      t.string :llm_url
      t.timestamps
    end
  end
end
