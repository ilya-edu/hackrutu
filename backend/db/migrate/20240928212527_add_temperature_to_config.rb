class AddTemperatureToConfig < ActiveRecord::Migration[7.1]
  def change
    add_column :configs, :temperature, :float
  end
end
