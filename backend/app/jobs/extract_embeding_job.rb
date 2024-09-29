class ExtractEmbedingJob < ApplicationJob
  queue_as :embeder
  queue_with_priority 2
  retry_on Errno::ECONNREFUSED, wait: 5, attempts: Float::INFINITY
  def perform(obj)
    return if obj.content_for_similarity.blank?
    obj.skip_embeding_update = true
    obj.update(embedding: TextEncoder.call(obj.content_for_similarity), search_index: obj.content_for_similarity)
  end
end
