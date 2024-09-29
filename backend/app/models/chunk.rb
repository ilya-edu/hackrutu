class Chunk < ApplicationRecord
  include EmbeddingExtractor
  belongs_to :article

  def content_for_similarity
    [content].compact.join(" ")
  end
end
