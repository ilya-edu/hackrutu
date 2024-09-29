class AddReferencesToMessage < ActiveRecord::Migration[7.1]
  def change
    add_column :messages, :references, :string, array: true
  end
end
