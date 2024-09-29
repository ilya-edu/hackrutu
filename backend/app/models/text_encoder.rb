require 'httparty'

class TextEncoder
  include HTTParty
  default_timeout 10.minutes.in_seconds
  base_uri ENV.fetch('ENCODER_URL')

  def self.call(text)
    response = post('/encode', body: { text: }.to_json, headers: { 'Content-Type' => 'application/json' })
    if response.success?
      response.parsed_response
    else
      { error: "Failed to encode text: #{response.message}" }
    end
  end
end
