class ParseChunksCsvJob < ApplicationJob
  def perform(file)
    csv = CSV.read(file)
    header = csv.shift
    csv.each do |line|
      Chunk.create(content: line[header.index("Content_Chunk")], article_id: line[header.index('Id')])
    end
  end
end