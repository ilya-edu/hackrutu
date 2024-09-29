require "active_support/concern"

module EmbeddingExtractor
  extend ActiveSupport::Concern

  included do
    attr_accessor :skip_embeding_update

    after_save_commit -> (obj) { ExtractEmbedingJob.perform_later(obj) unless skip_embeding_update }
    def content_for_similarity
      raise 'Content for similarity should be implemented'
    end
  end

end