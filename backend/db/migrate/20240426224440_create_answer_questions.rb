class CreateAnswerQuestions < ActiveRecord::Migration[7.1]
  def change
    create_table :answer_questions do |t|
      t.string :answer
      t.string :question
      t.string :category
      t.integer :answer_class
      t.vector :question_embedding, limit: 768
      t.timestamps
    end
  end
end
