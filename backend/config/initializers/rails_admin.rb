RailsAdmin.config do |config|
  config.asset_source = :sprockets
  class RailsAdmin::Config::Fields::Types::Vector < RailsAdmin::Config::Fields::Base
    RailsAdmin::Config::Fields::Types.register(self)
  end

  config.actions do
    dashboard                     # mandatory
    index do
      only %w[Message Room User Article Image VersionGroup Config Chunk]
    end
    new
    export
    bulk_delete
    show
    edit
    delete
    show_in_app

    config.model 'Article' do
      edit do
        field :name
        field :link
        field :content
        field :version
        field :version_group
        field :search_index
        field :images
      end
    end
    config.model 'Image' do
      edit do
        field :link
        field :content
        field :article
        field :search_index
        field :image
      end
    end
    config.model 'Message' do
      edit do
        field :user
        field :room
        field :text
        field :context
        field :references
      end
      list do
          field :user
          field :room
          field :text
      end
    end
  end
end
