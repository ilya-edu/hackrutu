class AddContextToMessage < ActiveRecord::Migration[7.1]
  def change
    add_column :messages, :context, :string
  end
end
