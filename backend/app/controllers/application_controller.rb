class ApplicationController < ActionController::Base
  before_action :dummy_auth
  protect_from_forgery with: :null_session
  def dummy_auth
    @current_user = User.find_or_create_by(name: params[:username])
  end
  attr_reader :current_user
end
