# LinkedIn Post Generator Skill

Transforms YouTube video subtitles into high-engagement LinkedIn posts optimized for software developer audiences.

## Quick Start

```
Use the linkedin-post-generator skill to create posts from video 25-12-05-kSdaDQh3TCw
```

Or more explicitly:

```
Generate LinkedIn posts from the subtitles in 25-12-05-kSdaDQh3TCw/download/
```

## What It Does

1. **Reads** your YouTube video subtitles (SRT files)
2. **Analyzes** content to extract 5 main topics relevant to software developers
3. **Asks** for your approval on the topics and strategy
4. **Generates** 3-4 LinkedIn posts per topic (15-20 total posts)
5. **Organizes** posts by topic in `{video-dir}/linkedin/` directory
6. **Creates** a posting schedule and tracking template

## Output Structure

```
25-12-05-kSdaDQh3TCw/
└── linkedin/
    ├── README.md                          # Overview & posting schedule
    ├── topic-1-canvas-tool-generation/
    │   ├── post-1-insight.md
    │   ├── post-2-story.md
    │   └── post-3-quick-tip.md
    ├── topic-2-deep-research/
    │   ├── post-1-insight.md
    │   ├── post-2-story.md
    │   └── post-3-contrarian.md
    ...
```

## Post Types Generated

Each topic gets multiple post variations:

- **Insight Posts**: Data-driven, surprising findings
- **Story Posts**: Personal experiences, case studies
- **Quick Tips**: Actionable takeaways
- **Contrarian Takes**: Challenge common beliefs
- **Discussion Posts**: Engagement-focused questions

## Strategy Alignment

Posts follow proven LinkedIn strategies:

✓ **Hook-first writing**: First 2 lines grab attention
✓ **Native content**: Optimized for LinkedIn algorithm
✓ **One idea per post**: Focused, digestible content
✓ **Mobile-optimized**: Short paragraphs, bullet points
✓ **Engagement-driven**: Ends with questions
✓ **Link strategy**: Links in comments, not main post

## Example Usage

### Basic

```
Generate LinkedIn posts from video kSdaDQh3TCw
```

### With Custom Options

```
Create LinkedIn posts from 25-12-05-kSdaDQh3TCw subtitles.
Use conversational tone and focus on AI/automation topics.
```

### For Specific Audience

```
Generate LinkedIn posts targeting senior software engineers
from the video in 25-12-05-kSdaDQh3TCw
```

## What Gets Created

For each post, you get:

```markdown
# [Post Title]

**Type**: Insight / Story / Quick Tip
**Target**: Software Developers
**Hashtags**: #SoftwareEngineering #TechCareers #AIAutomation
**Best Time**: Monday 8 AM

---

## Main Post

[Copy-paste ready LinkedIn post text]

---

## First Comment

[Link and engagement prompt to add as first comment]

---

## Engagement Strategy

- Respond to comments in first 2 hours
- Tag relevant connections
- Share in relevant groups

---

## Metrics to Track

- Impressions (goal: 2000+)
- Engagement rate (goal: 5%+)
- Comments (goal: 10+)
```

## Customization Options

The skill adapts to your preferences:

- **Tone**: Professional, conversational, technical, or mix
- **Length**: Short (200-300 words) or medium (400-500 words)
- **Emojis**: Yes, no, or sparingly
- **Focus**: Specific developer niches or general audience
- **Topics**: Approve or adjust the 5 main topics before generation

## Best Practices

### Before Generating

1. Ensure SRT file exists and contains good content
2. Review the video to understand key takeaways
3. Think about your target audience's pain points

### After Generating

1. Review all posts in the linkedin directory
2. Customize based on your personal voice
3. Add specific links to your blog/resources
4. Schedule posts using your preferred tool
5. Track engagement metrics

### When Posting

1. Post at optimal times (8 AM, 12 PM, 5 PM local)
2. Add link in first comment immediately
3. Respond to comments within 2 hours
4. Engage with others' content that day
5. Monitor which post types perform best

## Posting Schedule Template

The README.md will include a suggested schedule:

- **Week 1**: Topic 1 (Mon/Wed/Fri)
- **Week 2**: Topic 2 (Mon/Wed/Fri)
- **Week 3**: Topic 3 (Mon/Wed/Fri)
- **Week 4**: Topic 4 (Mon/Wed/Fri)
- **Week 5**: Topic 5 (Mon/Wed/Fri)

This gives you 1+ month of consistent LinkedIn content from a single video!

## Integration with Workflow

This skill works best as part of a content workflow:

1. Download YouTube video with subtitles (`youtube-downloader`)
2. **Generate LinkedIn posts** (`linkedin-post-generator`) ← This skill
3. Upload posts to LinkedIn using `scripts/linkedin_poster.py`
4. Track engagement and refine strategy

## Requirements

- YouTube video with English subtitles (SRT format)
- Located in standard directory structure: `{video-id}/download/*.srt`
- Familiarity with LinkedIn posting (or willingness to learn!)

## Tips for Maximum Engagement

1. **Consistency beats volume**: 2-3 quality posts/week > daily mediocre posts
2. **Engage before posting**: Comment on others' posts to warm up the algorithm
3. **Track what works**: Monitor which topics/formats get best engagement
4. **Refine your hook**: The first 2 lines make or break the post
5. **Build relationships**: Respond thoughtfully to every comment

## Troubleshooting

**No SRT file found?**
- Run youtube-downloader skill first to get subtitles

**Topics not relevant?**
- Adjust during the approval step
- Specify audience focus more clearly

**Posts too technical/simple?**
- Customize tone preference when asked
- Edit generated posts to match your voice

**Low engagement?**
- Review hook strength
- Post at better times
- Engage more with others' content first

## Next Steps

After generating posts:

1. Review the README.md in `{video-dir}/linkedin/`
2. Read through each post and customize as needed
3. Set up your posting schedule
4. Use `scripts/linkedin_poster.py` to post
5. Track results and iterate

## Examples

See `workflows/linkedin-posts-immigration-example.md` for sample posts created using this strategy.

## Related Resources

- **Strategy Guide**: `workflows/linkedin-repurposing-guide.md`
- **Posting Script**: `scripts/linkedin_poster.py`
- **Credential Setup**: `scripts/refresh_linkedin_credentials.py`

## Support

Questions or issues? Check:
1. The generated README.md in your video's linkedin directory
2. Example posts in workflows/linkedin-posts-immigration-example.md
3. Strategy guide in workflows/linkedin-repurposing-guide.md

---

**Pro Tip**: One high-quality video can generate 15-20 LinkedIn posts, giving you 1-2 months of consistent content. Focus on creating great source material!
