import pytest
from src.whisperyt import YouTubeTranscriber

# Insert API KEY to run test
API_KEY = "YOUR-API-KEY"
gladia = YouTubeTranscriber(API_KEY)

# checks response code of api request
def test_transcribe_video():
    response = gladia.transcribe("https://www.youtube.com/watch?v=BrcKRhQ7K00")
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main()