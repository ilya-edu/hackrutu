class AddExtraToAnswerQuestions < ActiveRecord::Migration[7.1]
  def change
    add_column :answer_questions, :extra, :boolean, default: false
  end
end
