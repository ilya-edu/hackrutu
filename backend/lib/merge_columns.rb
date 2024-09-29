
require 'csv'
require 'digest'
class MergeColumns
  def generate_hash(question, answer)
    # Create a hash by combining question and answer
    Digest::SHA256.hexdigest("#{question}#{answer}")
  end
  def perform
    # Define the input and output file paths
    input_file = 'lib/01_База_знаний.csv'
    output_file = 'lib/merged_output.csv'

    CSV.open(output_file, 'w') do |csv|
      # Write headers to the output file
      csv << ['Page', 'Content', 'Title', 'Category1', 'Category2']

      CSV.foreach(input_file, headers: true, col_sep: ',') do |row|
        # Extract the required columns
        tema = row['Тема']
        question = row['Вопрос из БЗ']
        answer = row['Ответ из БЗ']
        classifier_1 = row['Классификатор 1 уровня']
        classifier_2 = row['Классификатор 2 уровня']

        # Generate the hash
        hash_value = generate_hash(question, answer)

        # Merge the columns into a single string

        merged_column = "Пример Вопроса:\n #{question} \n\nПример ответа: \n #{answer}"
        # Write the new row to the output CSV
        csv << [hash_value, merged_column, answer, classifier_1, classifier_2]
      end
    end

    puts "CSV processing complete. Output saved to #{output_file}."
  end
end
