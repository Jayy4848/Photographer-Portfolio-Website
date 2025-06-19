from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from photographer.models import Category, GalleryImage, Testimonial, SiteSettings
# import requests  # Temporarily disabled for Vercel deployment
from datetime import date, datetime
import random


class Command(BaseCommand):
    help = 'Populate database with sample photography data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before adding new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            GalleryImage.objects.all().delete()
            Testimonial.objects.all().delete()
            Category.objects.all().delete()

        self.stdout.write('Creating sample data...')
        
        # Create or update site settings
        self.create_site_settings()
        
        # Create photography categories
        categories = self.create_categories()
        
        # Create sample gallery images for each category
        self.create_gallery_images(categories)
        
        # Create sample testimonials
        self.create_testimonials()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

    def create_site_settings(self):
        """Create or update site settings"""
        settings, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'photographer_name': 'Elite Photography Studio',
                'tagline': 'Capturing Life\'s Beautiful Moments with Artistic Vision',
                'about_text': 'We are professional photographers specializing in weddings, portraits, and events. With over 8 years of experience, we have captured thousands of precious moments for our clients. Our artistic approach combined with technical expertise ensures that every photo tells a story.',
                'email': 'contact@elitephotography.com',
                'phone': '+1 (555) 123-4567',
                'address': '123 Photography Street, Creative District, City 12345',
                'working_hours': 'Mon-Sat: 9AM-8PM, Sun: 10AM-6PM',
                'hero_title': 'Elite Photography Studio',
                'hero_subtitle': 'Creating timeless memories through cinematic photography',
                'meta_title': 'Elite Photography Studio - Professional Photography Services',
                'meta_description': 'Professional wedding, portrait, and event photography. Capturing your special moments with artistic vision and technical excellence.',
            }
        )
        if created:
            self.stdout.write('Created site settings')
        else:
            self.stdout.write('Site settings already exist')

    def create_categories(self):
        """Create photography categories"""
        categories_data = [
            {
                'name': 'Wedding Photography',
                'slug': 'wedding',
                'description': 'Capturing the magic of your special day with romantic and timeless wedding photography. From intimate ceremonies to grand celebrations, we document every precious moment of your love story.',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Pre-Wedding Shoots',
                'slug': 'pre-wedding',
                'description': 'Romantic pre-wedding photography sessions that capture your love story before the big day. Beautiful outdoor locations and intimate moments that showcase your relationship.',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Portrait Photography',
                'slug': 'portrait',
                'description': 'Professional portrait sessions that capture your personality and essence. Perfect for individuals, couples, and families with stunning lighting and composition.',
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Birthday Parties',
                'slug': 'birthday',
                'description': 'Fun and vibrant birthday party photography that captures all the joy, laughter, and celebration. From kids\' parties to milestone birthdays, we capture every smile.',
                'is_featured': False,
                'order': 4
            },
            {
                'name': 'Corporate Events',
                'slug': 'corporate',
                'description': 'Professional corporate photography for business events, conferences, product launches, and company portraits. Showcasing your business in the best light.',
                'is_featured': False,
                'order': 5
            },
            {
                'name': 'Baby & Family',
                'slug': 'family',
                'description': 'Precious moments with newborns, children, and families captured with care and creativity. Documenting the growth and love of your family.',
                'is_featured': False,
                'order': 6
            },
            {
                'name': 'Maternity Photography',
                'slug': 'maternity',
                'description': 'Beautiful maternity photography celebrating the journey to motherhood. Elegant and artistic photos that capture this special time in your life.',
                'is_featured': False,
                'order': 7
            },
            {
                'name': 'Graduation Photography',
                'slug': 'graduation',
                'description': 'Celebrating academic achievements with professional graduation photography. Capturing the pride and joy of this important milestone.',
                'is_featured': False,
                'order': 8
            },
            {
                'name': 'Fashion & Model',
                'slug': 'fashion',
                'description': 'High-fashion photography and modeling portfolios. Creative styling, dramatic lighting, and professional quality images for fashion industry.',
                'is_featured': False,
                'order': 9
            },
            {
                'name': 'Engagement Sessions',
                'slug': 'engagement',
                'description': 'Romantic engagement photography sessions that tell your love story. Beautiful locations and candid moments that celebrate your commitment.',
                'is_featured': False,
                'order': 10
            },
            {
                'name': 'Food Photography',
                'slug': 'food',
                'description': 'Professional food photography for restaurants, chefs, and culinary businesses. Making your dishes look irresistible with artistic presentation.',
                'is_featured': False,
                'order': 11
            },
            {
                'name': 'Sports Photography',
                'slug': 'sports',
                'description': 'Dynamic sports photography capturing the action, emotion, and intensity of athletic competitions and team events.',
                'is_featured': False,
                'order': 12
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        return categories

    def create_gallery_images(self, categories):
        """Create sample gallery images for each category"""
        
        # Sample image URLs with unique IDs for each category
        sample_images = {
            'wedding': [
                'https://picsum.photos/800/600?random=101',
                'https://picsum.photos/800/600?random=102',
                'https://picsum.photos/800/600?random=103',
                'https://picsum.photos/800/600?random=104',
                'https://picsum.photos/800/600?random=105',
                'https://picsum.photos/800/600?random=106',
                'https://picsum.photos/800/600?random=107',
                'https://picsum.photos/800/600?random=108',
                'https://picsum.photos/800/600?random=109',
                'https://picsum.photos/800/600?random=110',
                'https://picsum.photos/800/600?random=111',
                'https://picsum.photos/800/600?random=112',
            ],
            'pre-wedding': [
                'https://picsum.photos/800/600?random=201',
                'https://picsum.photos/800/600?random=202',
                'https://picsum.photos/800/600?random=203',
                'https://picsum.photos/800/600?random=204',
                'https://picsum.photos/800/600?random=205',
                'https://picsum.photos/800/600?random=206',
                'https://picsum.photos/800/600?random=207',
                'https://picsum.photos/800/600?random=208',
            ],
            'portrait': [
                'https://picsum.photos/800/600?random=301',
                'https://picsum.photos/800/600?random=302',
                'https://picsum.photos/800/600?random=303',
                'https://picsum.photos/800/600?random=304',
                'https://picsum.photos/800/600?random=305',
                'https://picsum.photos/800/600?random=306',
                'https://picsum.photos/800/600?random=307',
                'https://picsum.photos/800/600?random=308',
                'https://picsum.photos/800/600?random=309',
                'https://picsum.photos/800/600?random=310',
            ],
            'birthday': [
                'https://picsum.photos/800/600?random=401',
                'https://picsum.photos/800/600?random=402',
                'https://picsum.photos/800/600?random=403',
                'https://picsum.photos/800/600?random=404',
                'https://picsum.photos/800/600?random=405',
                'https://picsum.photos/800/600?random=406',
                'https://picsum.photos/800/600?random=407',
                'https://picsum.photos/800/600?random=408',
            ],
            'corporate': [
                'https://picsum.photos/800/600?random=501',
                'https://picsum.photos/800/600?random=502',
                'https://picsum.photos/800/600?random=503',
                'https://picsum.photos/800/600?random=504',
                'https://picsum.photos/800/600?random=505',
                'https://picsum.photos/800/600?random=506',
                'https://picsum.photos/800/600?random=507',
                'https://picsum.photos/800/600?random=508',
            ],
            'family': [
                'https://picsum.photos/800/600?random=601',
                'https://picsum.photos/800/600?random=602',
                'https://picsum.photos/800/600?random=603',
                'https://picsum.photos/800/600?random=604',
                'https://picsum.photos/800/600?random=605',
                'https://picsum.photos/800/600?random=606',
                'https://picsum.photos/800/600?random=607',
                'https://picsum.photos/800/600?random=608',
                'https://picsum.photos/800/600?random=609',
            ],
            'maternity': [
                'https://picsum.photos/800/600?random=701',
                'https://picsum.photos/800/600?random=702',
                'https://picsum.photos/800/600?random=703',
                'https://picsum.photos/800/600?random=704',
                'https://picsum.photos/800/600?random=705',
                'https://picsum.photos/800/600?random=706',
            ],
            'graduation': [
                'https://picsum.photos/800/600?random=801',
                'https://picsum.photos/800/600?random=802',
                'https://picsum.photos/800/600?random=803',
                'https://picsum.photos/800/600?random=804',
                'https://picsum.photos/800/600?random=805',
                'https://picsum.photos/800/600?random=806',
            ],
            'fashion': [
                'https://picsum.photos/800/600?random=901',
                'https://picsum.photos/800/600?random=902',
                'https://picsum.photos/800/600?random=903',
                'https://picsum.photos/800/600?random=904',
                'https://picsum.photos/800/600?random=905',
                'https://picsum.photos/800/600?random=906',
                'https://picsum.photos/800/600?random=907',
            ],
            'engagement': [
                'https://picsum.photos/800/600?random=1001',
                'https://picsum.photos/800/600?random=1002',
                'https://picsum.photos/800/600?random=1003',
                'https://picsum.photos/800/600?random=1004',
                'https://picsum.photos/800/600?random=1005',
                'https://picsum.photos/800/600?random=1006',
            ],
            'food': [
                'https://picsum.photos/800/600?random=1101',
                'https://picsum.photos/800/600?random=1102',
                'https://picsum.photos/800/600?random=1103',
                'https://picsum.photos/800/600?random=1104',
                'https://picsum.photos/800/600?random=1105',
                'https://picsum.photos/800/600?random=1106',
            ],
            'sports': [
                'https://picsum.photos/800/600?random=1201',
                'https://picsum.photos/800/600?random=1202',
                'https://picsum.photos/800/600?random=1203',
                'https://picsum.photos/800/600?random=1204',
                'https://picsum.photos/800/600?random=1205',
                'https://picsum.photos/800/600?random=1206',
            ]
        }

        # Image titles and descriptions for each category
        image_data = {
            'wedding': [
                ('Romantic Wedding Ceremony', 'Beautiful outdoor wedding ceremony captured during golden hour with stunning natural lighting'),
                ('Wedding Reception Dance', 'Joyful moments from the wedding reception dance floor showing pure happiness and celebration'),
                ('Bridal Portrait', 'Elegant bridal portrait showcasing the wedding dress and venue in perfect detail'),
                ('Wedding Rings Exchange', 'Intimate moment of ring exchange during the ceremony, capturing the emotion of commitment'),
                ('Wedding Party Photos', 'Fun group photos with the wedding party, bridesmaids and groomsmen in perfect harmony'),
                ('Wedding Venue Details', 'Beautiful venue decorations and setup details that complete the wedding story'),
                ('First Dance Moment', 'Romantic first dance as husband and wife under beautiful lighting'),
                ('Wedding Cake Cutting', 'Sweet moment of the couple cutting their wedding cake together'),
                ('Sunset Couple Portrait', 'Romantic couple portrait during sunset with breathtaking backdrop'),
                ('Wedding Bouquet Toss', 'Fun moment of bouquet toss with excited bridesmaids reaching for luck'),
                ('Wedding Ceremony Kiss', 'The magical first kiss as husband and wife sealing their vows'),
                ('Wedding Reception Toast', 'Heartfelt toast moment during reception with family and friends celebrating'),
            ],
            'pre-wedding': [
                ('Romantic Garden Session', 'Beautiful pre-wedding shoot in a romantic garden setting with natural flowers'),
                ('Beach Sunset Romance', 'Dreamy beach pre-wedding session during golden hour with waves in background'),
                ('Urban City Love', 'Modern pre-wedding shoot in urban city setting with architectural backdrop'),
                ('Vintage Style Romance', 'Classic vintage-themed pre-wedding session with timeless elegance'),
                ('Nature Trail Adventure', 'Adventure pre-wedding shoot on nature trails showing couple\'s adventurous side'),
                ('Cozy Home Session', 'Intimate pre-wedding session at home showing couple\'s daily life and love'),
                ('Mountain Top Romance', 'Breathtaking pre-wedding shoot on mountain top with panoramic views'),
                ('Cafe Date Session', 'Cute pre-wedding session at favorite cafe showing couple\'s sweet moments'),
            ],
            'portrait': [
                ('Professional Business Headshot', 'Corporate headshot with professional lighting perfect for LinkedIn and business use'),
                ('Artistic Studio Portrait', 'Creative studio portrait with dramatic lighting and artistic composition'),
                ('Family Portrait Session', 'Beautiful family portrait capturing the love and connection between family members'),
                ('Individual Creative Portrait', 'Unique individual portrait session with creative styling and personal touch'),
                ('Executive Professional Portrait', 'Distinguished executive portrait for corporate and professional use'),
                ('Lifestyle Portrait Session', 'Natural lifestyle portrait session showing personality in everyday setting'),
                ('Model Portfolio Portrait', 'Professional model portfolio portrait with perfect lighting and composition'),
                ('Senior Portrait Session', 'Memorable senior portrait session celebrating this important life milestone'),
                ('Couple Portrait Session', 'Romantic couple portrait session showing love and connection'),
                ('Children Portrait Session', 'Fun and natural children portrait session capturing their innocent joy'),
            ],
            'birthday': [
                ('Kids Birthday Party Fun', 'Joyful kids birthday party with colorful decorations and happy children playing'),
                ('Birthday Cake Celebration', 'Special moment of birthday cake cutting with candles and big smiles'),
                ('Party Games and Activities', 'Fun party activities and games with children having the time of their lives'),
                ('Birthday Girl/Boy Portrait', 'Special portrait of the birthday child in their party outfit looking adorable'),
                ('Family Birthday Gathering', 'Warm family gathering celebrating another year of life and love'),
                ('Milestone Birthday Celebration', 'Adult milestone birthday celebration with elegant decorations and joy'),
                ('Surprise Party Moment', 'Surprise birthday party moment capturing genuine shock and happiness'),
                ('Birthday Party Group Photo', 'Group photo of all party guests celebrating together with big smiles'),
            ],
            'corporate': [
                ('Business Conference Coverage', 'Professional coverage of business conference with speakers and attendees'),
                ('Corporate Team Building Event', 'Fun corporate team building event showing collaboration and teamwork'),
                ('Product Launch Presentation', 'Exciting product launch event with presentation and audience engagement'),
                ('Company Meeting Documentation', 'Professional business meeting documentation showing leadership and discussion'),
                ('Corporate Awards Ceremony', 'Prestigious corporate awards ceremony recognizing excellence and achievement'),
                ('Office Environment Portraits', 'Professional office environment portraits showing workplace culture'),
                ('Executive Team Photos', 'Formal executive team photos for company website and marketing materials'),
                ('Corporate Event Networking', 'Corporate networking event with professionals connecting and building relationships'),
            ],
            'family': [
                ('Family Outdoor Session', 'Beautiful family portrait session in outdoor natural setting with perfect lighting'),
                ('Newborn Baby Photography', 'Adorable newborn baby photography session capturing precious first moments'),
                ('Family Lifestyle Session', 'Natural family lifestyle session at home showing daily life and love'),
                ('Multi-Generation Portrait', 'Beautiful multi-generation family portrait showing family legacy and love'),
                ('Siblings Portrait Session', 'Fun siblings portrait session capturing the bond and love between brothers and sisters'),
                ('Family Holiday Session', 'Special family holiday session with festive decorations and joy'),
                ('Children Playing Session', 'Natural children photography session capturing them playing and having fun'),
                ('Parent and Child Bond', 'Intimate parent and child portrait showing the special bond and love'),
                ('Family Picnic Session', 'Fun family picnic session outdoors showing togetherness and happiness'),
            ],
            'maternity': [
                ('Elegant Maternity Portrait', 'Elegant maternity portrait celebrating the beauty of pregnancy and motherhood'),
                ('Outdoor Maternity Session', 'Beautiful outdoor maternity session in natural setting with soft lighting'),
                ('Couple Maternity Portrait', 'Sweet couple maternity portrait showing love and anticipation for baby'),
                ('Studio Maternity Photography', 'Professional studio maternity photography with artistic lighting and poses'),
                ('Lifestyle Maternity Session', 'Natural lifestyle maternity session at home showing anticipation and joy'),
                ('Maternity Silhouette Art', 'Artistic maternity silhouette photography creating beautiful wall art'),
            ],
            'graduation': [
                ('High School Graduation', 'Proud high school graduation moment with cap and gown and big smiles'),
                ('College Graduation Ceremony', 'College graduation ceremony coverage capturing this major life achievement'),
                ('Graduate Portrait Session', 'Professional graduate portrait session perfect for announcements and memories'),
                ('Family Graduation Celebration', 'Family celebration of graduation showing pride and love for the graduate'),
                ('Graduate Cap Throw', 'Traditional graduate cap throw moment with classmates celebrating together'),
                ('Diploma Presentation Moment', 'Special moment of diploma presentation during graduation ceremony'),
            ],
            'fashion': [
                ('High Fashion Editorial', 'High fashion editorial photography with dramatic styling and professional lighting'),
                ('Model Portfolio Session', 'Professional model portfolio session perfect for agency submissions'),
                ('Fashion Brand Campaign', 'Fashion brand campaign photography showcasing clothing and accessories beautifully'),
                ('Street Style Fashion', 'Urban street style fashion photography with modern and trendy looks'),
                ('Studio Fashion Photography', 'Professional studio fashion photography with perfect lighting and composition'),
                ('Lifestyle Fashion Session', 'Natural lifestyle fashion session showing clothing in everyday settings'),
                ('Beauty and Fashion Portrait', 'Beautiful beauty and fashion portrait highlighting makeup and styling'),
            ],
            'engagement': [
                ('Romantic Park Engagement', 'Romantic engagement session in beautiful park setting with natural scenery'),
                ('Urban Engagement Session', 'Modern urban engagement session with city architecture and lights'),
                ('Beach Engagement Shoot', 'Dreamy beach engagement session during sunset with waves and sand'),
                ('Home Engagement Session', 'Intimate home engagement session showing couple\'s personal space and love'),
                ('Adventure Engagement Shoot', 'Adventure engagement session showing couple\'s love for outdoor activities'),
                ('Vintage Engagement Session', 'Classic vintage-themed engagement session with timeless romantic feel'),
            ],
            'food': [
                ('Restaurant Menu Photography', 'Professional restaurant menu photography making dishes look irresistible'),
                ('Chef Portrait with Dishes', 'Professional chef portrait with signature dishes showcasing culinary artistry'),
                ('Food Styling and Photography', 'Artistic food styling and photography perfect for marketing and social media'),
                ('Bakery Product Photography', 'Beautiful bakery product photography showcasing fresh baked goods'),
                ('Fine Dining Experience', 'Elegant fine dining photography capturing the luxury dining experience'),
                ('Food Preparation Process', 'Behind-the-scenes food preparation photography showing culinary craft'),
            ],
            'sports': [
                ('Football Action Shot', 'Dynamic football action photography capturing the intensity of the game'),
                ('Basketball Game Coverage', 'Professional basketball game coverage showing athletic skill and teamwork'),
                ('Soccer Match Photography', 'Exciting soccer match photography capturing goals and celebrations'),
                ('Team Sports Portrait', 'Professional team sports portrait perfect for yearbooks and marketing'),
                ('Athletic Achievement Moment', 'Special moment of athletic achievement and victory celebration'),
                ('Sports Training Session', 'Sports training session photography showing dedication and hard work'),
            ]
        }

        locations = [
            'Downtown Studio', 'Central Park', 'Luxury Hotel', 'Beach Resort',
            'Garden Venue', 'Historic Mansion', 'Modern Gallery', 'Outdoor Pavilion',
            'Country Club', 'City Rooftop', 'Art Museum', 'Private Estate',
            'Mountain Lodge', 'Lakeside Venue', 'Urban Loft', 'Botanical Garden'
        ]

        for category_slug, category in categories.items():
            if category_slug in sample_images:
                urls = sample_images[category_slug]
                titles_descriptions = image_data[category_slug]
                
                for i, (url, (title, description)) in enumerate(zip(urls, titles_descriptions)):
                    # Create gallery image record
                    gallery_image = GalleryImage.objects.create(
                        title=title,
                        description=description,
                        category=category,
                        location=random.choice(locations),
                        date_taken=date.today(),
                        order=i + 1,
                        is_featured=i < 4  # First 4 images are featured
                    )
                    
                    self.stdout.write(f'Created image: {title} in {category.name}')

        self.stdout.write(f'Created {GalleryImage.objects.count()} sample images')

    def create_testimonials(self):
        """Create sample testimonials"""
        testimonials_data = [
            {
                'client_name': 'Sarah Johnson',
                'testimonial_text': 'Elite Photography Studio captured our wedding day perfectly! Every moment was beautifully documented, and the photos tell our love story better than we ever imagined. Highly recommended!',
                'event_type': 'Wedding Photography',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Michael Chen',
                'testimonial_text': 'The pre-wedding shoot was amazing! The photographer made us feel comfortable and captured our personalities perfectly. The photos are absolutely stunning and we treasure them forever.',
                'event_type': 'Pre-wedding Shoot',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'Emily Rodriguez',
                'testimonial_text': 'Professional, creative, and reliable! Our family portrait session was so much fun, and the photos are gorgeous. The photographer has an amazing eye for capturing natural moments.',
                'event_type': 'Family Photography',
                'rating': 5,
                'is_featured': True,
            },
            {
                'client_name': 'David Thompson',
                'testimonial_text': 'Outstanding corporate event photography! The team captured our product launch perfectly, and the photos are being used across all our marketing materials. Exceptional quality!',
                'event_type': 'Corporate Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Lisa Williams',
                'testimonial_text': 'The maternity photoshoot was a wonderful experience! The photographer made me feel beautiful and confident, and the photos are absolutely magical. Perfect memories of this special time.',
                'event_type': 'Maternity Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'James Wilson',
                'testimonial_text': 'My daughter\'s graduation photos are perfect! The photographer captured this milestone beautifully, and we now have stunning portraits to commemorate her achievement.',
                'event_type': 'Graduation Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Amanda Davis',
                'testimonial_text': 'The engagement session exceeded our expectations! The photos are romantic, artistic, and perfectly capture our love. We can\'t wait to work with them for our wedding!',
                'event_type': 'Engagement Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Robert Martinez',
                'testimonial_text': 'Fantastic fashion photography for our brand campaign! The photographer understood our vision perfectly and delivered images that showcase our products beautifully.',
                'event_type': 'Fashion Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Jennifer Brown',
                'testimonial_text': 'The birthday party coverage was incredible! Every smile, every laugh, every special moment was captured perfectly. Our family will treasure these photos forever.',
                'event_type': 'Birthday Photography',
                'rating': 5,
                'is_featured': False,
            },
            {
                'client_name': 'Chris Taylor',
                'testimonial_text': 'Professional sports photography at its finest! The action shots from our tournament are amazing, and the team photos look fantastic. Highly recommend for any sports event!',
                'event_type': 'Sports Photography',
                'rating': 5,
                'is_featured': False,
            }
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'Created testimonial from: {testimonial.client_name}')

        self.stdout.write(f'Created {Testimonial.objects.count()} testimonials') 