class ParseArticlesJob < ApplicationJob
  queue_as :parsers
  def perform(file)
    csv = CSV.parse(file)
    headers = csv.shift
    csv.each do |line|
      link = line[headers.index('Page')]
      content = line[headers.index('Content')]
      title = line[headers.index('Title')]
      category1 = line[headers.index('Category1')]
      category2 = line[headers.index('Category2')]
      article = Article.create(link:, content: content, name: title, category1: category1, category2: category2 )
      content.gsub(/\s+/, ' ').scan(/.{1,2000}(?: |$)/).map(&:strip).each do |chunk|
        Chunk.create(article:, content: chunk)
      end
    end
  end
end