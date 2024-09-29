class AddllmEnableToprompts < ActiveRecord::Migration[7.1]
  def change
    rename_table :prompts, :configs
    add_column :configs, :llm_enabled, :boolean, default: false
  end
end
