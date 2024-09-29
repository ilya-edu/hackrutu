module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
      logger.add_tags 'ActionCable', current_user.id
    end

    private
    def find_verified_user
      User.find_or_create_by(name: request.params[:username])
    end
  end
end