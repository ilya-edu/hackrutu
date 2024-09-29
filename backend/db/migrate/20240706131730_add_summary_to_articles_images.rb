class AddSummaryToArticlesImages < ActiveRecord::Migration[7.1]
  def change
    add_column :articles, :summary, :text
    add_column :images, :summary, :text
  end
end
