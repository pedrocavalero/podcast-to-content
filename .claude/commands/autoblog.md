Execute the YouTube to WordPress autoblog workflow from `workflows/autoblog.workflow.md` for YouTube video ID: {{video_id}} with {{num_posts}} blog posts.

Follow each step in the workflow carefully, adapting the number of posts as specified:

1. Ask for the YouTube video ID if not provided
2. Create the `blog-{VIDEO_ID}` directory
3. Run transcription: `source .venv/bin/activate && python3 transcribe.py {VIDEO_ID} -s >> blog-{VIDEO_ID}/transcript.txt`
4. Analyze and summarize content - identify the top topics based on the number of posts requested
5. Generate the specified number of blog posts following the content guidelines
6. Review and refine each post (quote cleanup, grammar, tone)
7. Generate featured images for each post
8. Publish all posts to WordPress

Important:
- Stop the workflow if any critical step fails (transcription, post generation, image generation)
- Save all outputs to the `blog-{VIDEO_ID}` directory
- Use Python scripts in `scripts/` directory with the virtual environment activated
- Follow the content guidelines exactly as specified in the workflow document
- Ensure all quotes are cleaned up (remove filler words, fix grammar) while preserving meaning
- Sign all posts as "Pedro Cavalero"
