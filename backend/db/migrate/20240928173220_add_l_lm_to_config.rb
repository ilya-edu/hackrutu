class AddLLmToConfig < ActiveRecord::Migration[7.1]
  def change
    add_column :configs, :llm, :string
  end
end
