Rails.application.routes.draw do
  mount RailsAdmin::Engine => '/admin', as: 'rails_admin'
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html
  mount GoodJob::Engine => 'good_job'
  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check
  mount ActionCable.server => "/cable"
  # Defines the root path route ("/")
  # root "posts#index"
  resources :answer_questions, only: %w[index new create] do
    collection do
      post :batch_search
      get :upload_batch_search
    end
  end
  resources :submits, only: %w[show]
  resources :rooms, only: %w[index show destroy]
  resources :messages, only: %w[index create]
  resources :chunks, only: %w[index new create]
  resources :articles, only: %w[index new create show]
  post '/predict', to: 'predict#predict'
end
