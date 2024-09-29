class ChangeVectorSize < ActiveRecord::Migration[7.1]
  def change
    remove_column :answer_questions, :question_embedding
    add_column :answer_questions, :question_embedding, :vector
  end
end
