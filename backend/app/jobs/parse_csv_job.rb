class ParseCsvJob < ApplicationJob
  def perform(*)
    csv = CSV.read('public/articles.csv')
    headers = csv.shift
    csv.each do |line|
      link = line[headers.index('Page')]
      content = line[headers.index('Content')]
      title = line[headers.index('Title')]
      Article.create(link:, content: content.delete("\0"), name: title )
    end

    csv = CSV.read('public/images.csv')
    headers = csv.shift
    csv.each do |line|
      article = Article.find_by_link(line[headers.index('Page')])
      image_url = line[headers.index('Image')]
      content = line[headers.index('Content')]
      Image.create(article:, content:, link: image_url  )
    end


  end
end
# downloaded_image = open("http://www.example.com/image.jpg")
# self.avatar.attach(io: downloaded_image  , filename: "foo.jpg")