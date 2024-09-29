class Image < ApplicationRecord
  include EmbeddingExtractor
  belongs_to :article
  has_one_attached :image
  def content_for_similarity
    [content, link].compact.join(' ')
  end
end