class Article < ApplicationRecord
  belongs_to :version_group, class_name: 'VersionGroup', optional: true
  has_many :images
  has_many :chunks, dependent: :destroy
  def content_for_similarity
    [name, content, version.present? ? "Версия: #{version}" : nil ].compact.join(" ")
  end
end