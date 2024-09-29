class User < ApplicationRecord
  has_many :messages
  has_many :rooms, through: :messages

  def admin?
    name == 'admin'
  end
  def self.admin
    find_by(name: 'admin') || create(name: 'admin')
  end
  def self.llm
    find_by(name: 'llm') || create(name: 'llm')
  end
  def self.tester
    find_by(name: 'tester') || create(name: 'tester')
  end
end
