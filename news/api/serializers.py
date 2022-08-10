from rest_framework import serializers
from datetime import datetime, date
from django.utils.timesince import timesince
from news.models import Article, Journalist


class ArticleSerializerDefault(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    main_text = serializers.CharField()
    published_time = serializers.DateField()
    is_active = serializers.BooleanField()
    created_time = serializers.DateTimeField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.main_text = validated_data.get('main_text', instance.main_text)
        instance.published_time = validated_data.get('published_time', instance.published_time)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and Description cannot be same!')
        return data

    def validate_title(self, title):
        if len(title) < 8:
            raise serializers.ValidationError(f'Title must be minimum 8 characters,\
                                              you entered {len(title)} characters')


class ArticleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    # author = JournalistSerializer()

    def get_time_since_pub(self, publish_time):
        now = datetime.now()
        pub_time = publish_time.published_time
        time_delta = timesince(pub_time, now)
        return time_delta

    def validate_published_time(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError("This is a date that has not come yet!")
        return value

    class Meta:
        model = Article
        # fields = '__all__'
        # fields = ['id', 'title', 'author', 'description', 'main_text', 'published_time']
        exclude = ['title']
        read_only_fields = ['created_time', 'id', 'updated_time']


class JournalistSerializer(serializers.ModelSerializer):
    # articles = ArticleSerializer(read_only=True, many=True)
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article_list_detail',
    )

    class Meta:
        model = Journalist
        fields = '__all__'
