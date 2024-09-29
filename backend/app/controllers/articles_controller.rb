class ArticlesController < ApplicationController


  def new;end

  def show
    @article = Article.find_by(link: params[:id])
  end
  def create
    file = params[:file_upload]
    ParseArticlesJob.perform_later(file.read.delete("\0"))
  end

  def upload_batch_search
    @submits = Submit.all.order(created_at: :desc)
  end

  def index
    @chunks = SemanticSearch.new.perform(query, :chunks)
  end

  def query
    params[:query] || ' '
  end

end
