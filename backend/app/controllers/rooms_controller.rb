class RoomsController < ApplicationController
  def index
    Room.main.joins(:messages)
        .where('messages.id IN (
                      SELECT MAX(messages.id)
                      FROM messages
                      GROUP BY messages.room_id
                    )')
        .where.not(messages: { user_id: User.admin.id }).update_all(human_need: true)

    @rooms = current_user.admin? ? Room.main.includes(:messages) : Room.main.includes(:messages).where(messages: {user: current_user} )
  end
  def destroy
    Room.find(params[:id]).destroy
    head :no_content
  end
end