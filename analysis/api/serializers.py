from rest_framework import serializers
from file.models import File
from analysis.models import Analysis
from user.models import User
ANALYSIS = (
    ('descriptive_statistic', 'descriptive_statistic'),
    ('random_number_generation', 'random_number_generation'),
    ('correlation', 'correlation'),
    ('covariance', 'covariance'),
    ('anova_single_factor', 'anova_single_factor'),
    ('anova_2_factor_with_replication', 'anova_2_factor_with_replication'),
    ('anova_2_factor_without_replication', 'anova_2_factor_without_replication'),
    ('t_test_2_sample_assuming_equal_variances',
     't_test_2_sample_assuming_equal_variances'),
    ('t_test_2_sample_assuming_unequal_variances',
     't_test_2_sample_assuming_unequal_variances'),
    ('t_test_2_sample_for_means', 't_test_2_sample_for_means'),
    ('simple_linear_regression', 'simple_linear_regression'),
    ('non_linear_regression', 'no_linear_regression'),
    ('polynomial_regression', 'polynomial_regression'),
    ("multiple_linear_regression", "multiple_linear_regression"),
    ('exponential_smoothing', 'exponential_smoothing'),
    ('moving_average', 'moving_average'),
)

class FileResponeSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

class CreatedBySerilizer(serializers.ModelSerializer):
    
    class Meta:
        
        model= User
        fields= ["username","full_name","avatar","uuid","is_deleted","email"]

class AnalysisSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    model_name = serializers.ChoiceField(choices=ANALYSIS)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = ("__all__")

    def get_user(self, obj):

        user = obj.user
        serializer = CreatedBySerilizer(user)
        return serializer.data

    def get_file(self, obj):
        try:
            file = File.objects.get(filename=obj.filename)  # or use the appropriate filter
            return FileResponeSerializer(file).data
        except File.DoesNotExist:
            return None


class AnalysisUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysis
        fields = ["thumbnail", "title"]



visualize = (
    ("scatter_plot", "scatter_plot"),
    ("histogram", "histogram"),
    ("boxplot", "boxplot"),
    ("line_chart", "line_chart"),
)


class ExploratoryDataAnalysisSerializer(serializers.Serializer):
    independent_variable = serializers.CharField( required=True)
    dependent_variable = serializers.CharField( required=True)
    filename = serializers.CharField(max_length=200, required=True)
    visualizes = serializers.MultipleChoiceField(
        choices=visualize, required=True)


class DescriptiveStatisticsSerializer(serializers.Serializer):
    filename = serializers.CharField( required=True)


class RandomNumberGenerationSerializer(serializers.Serializer):
    independent_variable = serializers.CharField( required=True)
    dependent_variable = serializers.CharField( required=True)
    filename = serializers.CharField( required=True)


class CorrelationSerializer(serializers.Serializer):
    independent_variable = serializers.CharField( required=True)
    dependent_variable = serializers.CharField( required=True)
    filename = serializers.CharField( required=True)


class CovarianceSerializer(serializers.Serializer):
    independent_variable = serializers.CharField( required=True)
    dependent_variable = serializers.CharField( required=True)
    filename = serializers.CharField( required=True)


class SimpleLinearRegressionSerializer(serializers.Serializer):
    filename = serializers.CharField( required=True)
    independent_variable = serializers.CharField( required=True)
    dependent_variable = serializers.CharField( required=True)
    predict_values = serializers.IntegerField(default=200)


class NonLinearRegressionSerializer(serializers.Serializer):
    filename = serializers.CharField()
    independent_variable = serializers.CharField()
    dependent_variable = serializers.CharField()
    degree = serializers.IntegerField(default=2)
    predict_values = serializers.IntegerField(default=200)


class MultipleLinearRegressionSerializer(serializers.Serializer):
    filename = serializers.CharField( required=True)
    independent_variables = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of names of independent variables",
        required=True
    )
    dependent_variable = serializers.CharField(
        help_text="Name of the dependent variable")

    def validate_independent_variables(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Multiple linear regression requires at least two independent variables.")
        return value
class T_TestOneSample(serializers.Serializer):
    filename = serializers.CharField( required=True)
    hypothesis_mean_column = serializers.CharField(required=True)
    sample_mean = serializers.FloatField(
        help_text="Name of the dependent variable")
    
class AnovaSingleFactorSerializer(serializers.Serializer):
    filename = serializers.CharField( required=True)
    list_range_numeric = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of names of range variables and numeric only variables",
        required=True
    )

class TwoSampleTTest(serializers.Serializer):
    filename = serializers.CharField( required=True)
    independent_variables = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of names of independent variables",
        required=True
    )

    def validate_independent_variables(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Multiple linear regression requires at least two independent variables.")
        return value

class TwoSamplePairedTTest(serializers.Serializer):
    filename = serializers.CharField( required=True)
    list_paired_samples = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of names of independent variables",
        required=True
    )


    def validate_independent_variables(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Multiple linear regression requires at least two independent variables.")
        return value


class ExponentialSmoothingSerializer(serializers.Serializer):
    filename = serializers.CharField( required=True)
    number_of_day_to_forecast = serializers.IntegerField(required=True)
    column_date = serializers.CharField(required=True)
    number_column = serializers.CharField(required=True)


class PerformAnalysisSerializer(serializers.ModelSerializer):
    MODEL_CHOICES = [
        ('descriptive_statistic', DescriptiveStatisticsSerializer),
        ('random_number_generation', RandomNumberGenerationSerializer),
        ('correlation', CorrelationSerializer),
        ('covariance', CovarianceSerializer),
        ('simple_linear_regression', SimpleLinearRegressionSerializer),
        ('non_linear_regression', NonLinearRegressionSerializer),
        ('multiple_linear_regression', MultipleLinearRegressionSerializer),
        ('one_way_anova',AnovaSingleFactorSerializer),
        ('two_way_anova',MultipleLinearRegressionSerializer),
        ("one_sample_t_test",T_TestOneSample),
        ("two_sample_t_test",TwoSampleTTest),
        ("paired_t_test",TwoSamplePairedTTest),
        ("exponential_smoothing", ExponentialSmoothingSerializer),
    ]


    model_name = serializers.ChoiceField(choices=MODEL_CHOICES)
    class Meta:
        model = Analysis
        fields = ("__all__")
    def to_internal_value(self, data):
        model_name = data.get('model_name')
        if model_name in dict(self.MODEL_CHOICES):
            serializer_class = dict(self.MODEL_CHOICES)[model_name]
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return {'model_name': model_name, **serializer.validated_data}
        else:
            raise serializers.ValidationError({"model_name": "Invalid model name."})

    def to_representation(self, instance):
        model_name = instance.get('model_name')
        if model_name in dict(self.MODEL_CHOICES):
            serializer_class = dict(self.MODEL_CHOICES)[model_name]
            serializer = serializer_class(instance)
            return {'model_name': model_name, **serializer.data}
        return {'model_name': model_name}




