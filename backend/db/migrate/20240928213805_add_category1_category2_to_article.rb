class AddCategory1Category2ToArticle < ActiveRecord::Migration[7.1]
  def change
    add_column :articles, :category1, :string
    add_column :articles, :category2, :string
  end
end
