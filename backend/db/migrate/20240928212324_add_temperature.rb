class AddTemperature < ActiveRecord::Migration[7.1]
  def change
    add_column :messages, :temperature, :float
  end
end
