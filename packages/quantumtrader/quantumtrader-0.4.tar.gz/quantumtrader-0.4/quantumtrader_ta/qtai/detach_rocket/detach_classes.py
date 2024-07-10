"""使用随机卷积核进行时间序列分类的顺序特征选择

时间序列分类（TSC）能够实现异常检测和股票价格分析等任务

在这里，我们引入了顺序特征分离（SFD），以识别和剪枝基于ROCKET的模型（如ROCKET、MiniRocket和MultiRocket）中的非必要特征

SFD:用于在TSC中顺序选择和剪枝由随机卷积核变换生成的特征。利用分类器的线性特性，我们的方法在每一步使用模型系数估计特征重要性。与先前的稀疏回归背景下开发的阈值最小二乘法（STLSQ）和逐步稀疏回归器（SSR）等特征选择算法不同，SFD旨在有效处理具有大型特征集的任务，并消除了对敏感超参数选择的需求

github：https://github.com/gon-uri/detach_rocket/tree/main

"""

from .utils import (feature_detachment, select_optimal_model,
                    retrain_optimal_model)

from sklearn.linear_model import (RidgeClassifierCV, RidgeClassifier)
from sklearn.preprocessing import StandardScaler
from sktime.transformations.panel.rocket import (Rocket,
                                                 MiniRocketMultivariate,
                                                 MultiRocketMultivariate)
from sklearn.model_selection import train_test_split
import numpy as np


class DetachRocket:
    """
    特征分离功能的Rocket（随机卷积核转换）模型，用于识别和保留对模型预测最重要的特征

    - 对于单变量时间序列数据，训练数据集`X_train`的形状应该是二维数组，其中第一维`n_timepoints`代表每个时间序列中的时间点，第二维`n_instances`代表时间序列的实例数量。`(n_instances, n_timepoints)`
    
        简单来说，这是说对于单个时间序列的每个实例，我们有一系列时间点的观测值

    - 对于多变量时间序列数据，训练数据集`X_train`的形状应该是三维数组，其中第一维`n_timepoints`是每个变量中的时间点数量。第二维`n_instances`同样是时间序列实例的数量，第三维`n_variables`代表时间序列中变量的数量，`(n_instances, n_variables, n_timepoints)`

        这意味着对于多个时间序列的每个实例，我们有多个变量，每个变量都有一系列的时间点观测值

    - rocket训练时，X的要求是三维的（3D numpy.ndarray） 形状为 `[n_instances, n_dimensions, series_length]`，其中`n_instances`表示实例数量，`n_dimensions`表示维度数（或通道数，对于多变量时间序列），`series_length`表示每个时间序列的长度,因此需要：

    >>> X_train = X_train.values.reshape(X_train.shape[0],1,X_train.shape[1]) 
    >>> X_test = X_test.values.reshape(X_test.shape[0],1,X_test.shape[1])

    ### 参数：
    - model_type: Rocket模型的类型，可以是"rocket"-随机卷积核转换、"minirocket"-简单随机卷积核转换 或"multirocket"-多向随机卷积核转换。
    - num_kernels: Rocket模型中的核（kernels）数量。
    - trade_off: 用于设置最优剪枝（pruning）的权衡参数。
    - recompute_alpha: 是否重新计算alpha以进行最优模型训练。
    - val_ratio: 验证集的比例。
    - verbose: 日志记录的详细程度。
    - multilabel_type: 在多标签分类情况下的特征排名类型，默认为"max"。
    - fixed_percentage: 如果不是None，将忽略trade_off参数，并使用固定百分比的特征来拟合模型。
    
    ### 属性：
    - _sfd_curve: 顺序特征分离的曲线。
    - _full_transformer: Rocket模型的完整变换器。
    - _full_classifier: 基线模型的完整分类器。
    - _full_model_alpha: 完整模型的Alpha值。
    - _classifier: 最优模型的分类器。
    - _feature_matrix: 特征矩阵。
    - _feature_importance_matrix: 特征重要性矩阵，零值表示被剪枝的特征。维度：[步数，特征数]。
    - _percentage_vector: 百分比值向量。
    - _scaler: 特征矩阵的缩放器。
    - _labels: 标签。
    - _acc_train: 训练准确度。
    - _max_index: 最大百分比的索引。
    - _max_percentage: 最大百分比。
    - _is_fitted: 指示模型是否已经拟合的标记。
    - _optimal_computed: 指示最优模型是否已计算的标记。
    
    ### 方法：
    - fit: 拟合DetachRocket模型。
    - fit_trade_off: 使用给定的权衡参数拟合模型。
    - fit_fixed_percentage: 使用固定百分比的特征拟合模型。
    - predict: 使用拟合的模型进行预测。
    - score: 获取模型的准确度分数。

    """

    def __init__(self,
                 model_type='rocket',
                 num_kernels=10000,
                 trade_off=0.1,
                 recompute_alpha=True,
                 val_ratio=0.33,
                 verbose=False,
                 multilabel_type='max',
                 fixed_percentage=None):

        self._sfd_curve = None
        #self._transformer = None
        self._full_transformer = None
        self._full_classifier = None
        self._full_model_alpha = None
        self._classifier = None
        self._feature_matrix = None
        self._feature_matrix_val = None
        self._feature_importance_matrix = None
        self._percentage_vector = None
        self._scaler = None
        self._labels = None
        self._acc_train = None
        self._max_index = None
        self._max_percentage = None
        self._is_fitted = False
        self._optimal_computed = False

        self.num_kernels = num_kernels
        self.trade_off = trade_off
        self.val_ratio = val_ratio
        self.recompute_alpha = recompute_alpha
        self.verbose = verbose
        self.multilabel_type = multilabel_type
        self.fixed_percentage = fixed_percentage

        # 创建 rocket 模型
        if model_type == "rocket":
            self._full_transformer = Rocket(num_kernels=num_kernels)
        elif model_type == "minirocket":
            self._full_transformer = MiniRocketMultivariate(
                num_kernels=num_kernels)
        elif model_type == "multirocket":
            self._full_transformer = MultiRocketMultivariate(
                num_kernels=num_kernels)
        else:
            raise ValueError(
                '无效的model_type参数。可选:“rocket”、“minirocket”或“multirocket”')

        # 分类和特征缩放
        # 岭回归（Ridge Regression）分类，通过添加L2正则化项（也称为权重衰减）来减少模型的复杂度，避免过拟合
        # StandardScaler()改善算法的表现和收敛速度，用于特征中心化和缩放的标准缩放器
        self._full_classifier = RidgeClassifierCV(
            alphas=np.logspace(-10, 10, 20))
        self._scaler = StandardScaler(with_mean=True)

        return

    def fit(self,
            X,
            y=None,
            val_set=None,
            val_set_y=None,
            X_test=None,
            y_test=None):

        assert y is not None, "要拟合（训练）分离随机卷积核转换（Detach Rocket）模型，必须提供标签"

        if self.fixed_percentage is not None:
            # 如果提供了固定百分比，则不需要验证集
            # 强调提醒没有验证集
            assert val_set is None, "当使用固定比例的特征时，不允许使用验证集，因为训练过程中不需要它"
            # 强调提醒已经提供了测试集 X_test 和相应的测试标签 y_test
            assert X_test is not None, "X_test 是必需的，以使用固定比例来拟合（或说是分析）分离随机卷积核转换（D-Rocket），但它不是用于训练的，而是用于绘制特征分离曲线（feature detachment curve）"
            assert y_test is not None, "y_test 在使用固定比例拟合分离随机卷积核转换（D-Rocket）时是必需的。它不是用于训练的，而是用于绘制特征脱离曲线的"

        if self.verbose == True:
            print('数据转换')

        self._feature_matrix = self._full_transformer.fit_transform(X)
        self._labels = y

        if self.verbose == True:
            print('拟合完整模型')

        # 缩放特征矩阵
        self._feature_matrix = self._scaler.fit_transform(self._feature_matrix)

        if val_set is not None:
            self._feature_matrix_val = self._full_transformer.transform(
                val_set)
            self._feature_matrix_val = self._scaler.transform(
                self._feature_matrix_val)

        # 训练基准
        self._full_classifier.fit(self._feature_matrix, y)
        self._full_model_alpha = self._full_classifier.alpha_

        print('随机卷积核转换（ROCKET）-训练结果:')
        print('最佳Alpha: {:.2f}'.format(self._full_model_alpha))
        print('训练准确率: {:.2f}%'.format(
            100 * self._full_classifier.score(self._feature_matrix, y)))
        print('-------------------------')

        # 如果没有提供固定百分比，我们将使用验证集来设置特征的数量。
        if self.fixed_percentage is None:
            assert X_test is None, "在使用权衡曲线（trade-off curves）时，不允许使用测试集（X_test），权衡曲线是使用验证集计算的。"

            if val_set is not None:
                X_train = self._feature_matrix
                X_val = self._feature_matrix_val
                y_train = y
                y_val = val_set_y
            else:
                # Train-Validation split
                X_train, X_val, y_train, y_val = train_test_split(
                    self._feature_matrix,
                    y,
                    test_size=self.val_ratio,
                    random_state=42,
                    stratify=y)

            # 为选定的特征训练模型
            sfd_classifier = RidgeClassifier(alpha=self._full_model_alpha)
            sfd_classifier.fit(X_train, y_train)

            # 特征分离
            if self.verbose == True:
                print('序列特征分离')

            self._percentage_vector, _, self._sfd_curve, self._feature_importance_matrix = feature_detachment(
                sfd_classifier,
                X_train,
                X_val,
                y_train,
                y_val,
                verbose=self.verbose,
                multilabel_type=self.multilabel_type)

            self._is_fitted = True

            # 训练最优模型
            if self.verbose == True:
                print('训练最优模型')

            self.fit_trade_off(self.trade_off)

        else:
            # 如果提供了固定百分比，则不需要验证集
            # 我们不需要将数据分成训练和验证
            # 我们使用固定比例的功能
            X_train = self._feature_matrix
            y_train = y
            X_test = self._scaler.transform(
                self._full_transformer.transform(X_test))

            # 为选定的特征训练模型
            sfd_classifier = RidgeClassifier(alpha=self._full_model_alpha)
            sfd_classifier.fit(X_train, y_train)

            # 特征分离
            if self.verbose == True:
                print('Applying Sequential Feature Detachment')

            self._percentage_vector, _, self._sfd_curve, self._feature_importance_matrix = feature_detachment(
                sfd_classifier,
                X_train,
                X_test,
                y_train,
                y_test,
                verbose=self.verbose,
                multilabel_type=self.multilabel_type)

            self._is_fitted = True

            if self.verbose == True:
                print('Using fixed percentage of features')
            self.fit_fixed_percentage(self.fixed_percentage)

        return

    def fit_trade_off(self, trade_off=None):

        assert trade_off is not None, "Missing argument"
        assert self._is_fitted == True, "模型未进行训练。首先调用fit方法"

        # 选择最优
        max_index, max_percentage = select_optimal_model(
            self._percentage_vector,
            self._sfd_curve,
            self._sfd_curve[0],
            self.trade_off,
            graphics=False)
        self._max_index = max_index
        self._max_percentage = max_percentage

        # 检查alpha是否会被重新计算
        if self.recompute_alpha:
            alpha_optimal = None
        else:
            alpha_optimal = self._full_model_alpha

        # 创建特征蒙版
        self._feature_mask = self._feature_importance_matrix[max_index] > 0

        # 重新训练最优模型
        self._classifier, self._acc_train = retrain_optimal_model(
            self._feature_mask,
            self._feature_matrix,
            self._labels,
            self._max_index,
            alpha_optimal,
            verbose=self.verbose)

        return

    def fit_fixed_percentage(self, fixed_percentage=None, graphics=True):

        assert fixed_percentage is not None, "Missing argument"
        assert self._is_fitted == True, "模型未进行训练。首先调用fit方法"

        self._max_index = (np.abs(self._percentage_vector -
                                  self.fixed_percentage)).argmin()
        self._max_percentage = self._percentage_vector[self._max_index]

        # Check if alpha will be recomputed
        if self.recompute_alpha:
            alpha_optimal = None
        else:
            alpha_optimal = self._full_model_alpha

        # Create feature mask
        self._feature_mask = self._feature_importance_matrix[
            self._max_index] > 0

        # Re-train optimal model
        self._classifier, self._acc_train = retrain_optimal_model(
            self._feature_mask,
            self._feature_matrix,
            self._labels,
            self._max_index,
            alpha_optimal,
            verbose=self.verbose)

        return

    def predict(self, X):

        assert self._is_fitted == True, "模型未进行训练。首先调用fit方法"

        # Transform time series to feature matrix
        transformed_X = np.asarray(self._full_transformer.transform(X))
        transformed_X = self._scaler.transform(transformed_X)
        masked_transformed_X = transformed_X[:, self._feature_mask]

        y_pred = self._classifier.predict(masked_transformed_X)

        return y_pred

    def score(self, X, y):

        assert self._is_fitted == True, "模型未进行训练。首先调用fit方法"

        # Transform time series to feature matrix
        transformed_X = np.asarray(self._full_transformer.transform(X))
        transformed_X = self._scaler.transform(transformed_X)
        masked_transformed_X = transformed_X[:, self._feature_mask]

        return self._classifier.score(masked_transformed_X,
                                      y), self._full_classifier.score(
                                          transformed_X, y)


class DetachMatrix:
    """
    特征脱离（Sequential Feature Detachment, SFD）方法来修剪特征矩阵

    适用于处理形状为`(n_instances, n_features)`的特征矩阵，其中`n_instances`是样本数量，`n_features`是特征数量 `(n_instances, n_features)`

    ### 参数
    - `trade_off`: 权衡参数，用于在特征数量与模型精度之间做出权衡。
    - `recompute_alpha`: 布尔值，指定是否在最优模型训练中重新计算alpha（正则化参数）。
    - `val_ratio`: 验证集比例，用于划分训练集和验证集。
    - `verbose`: 布尔值，控制日志输出的详细程度。
    - `multilabel_type`: 多标签分类的类型，默认为`"max"`，表示在多类问题中如何确定特征重要性。
    ### 属性
    - `_sfd_curve`: 顺序特征脱离过程的曲线数据。
    - `_scaler`: 用于特征矩阵的缩放器。
    - `_classifier`: 最优模型的分类器。
    - `_acc_train`: 训练集上的准确率。
    - `_full_classifier`: 用于基线比较的完整分类器。
    - `_percentage_vector`: 百分比值向量，表示不同步骤中特征保留的比例。
    - `_feature_matrix`: 特征矩阵。
    - `_labels`: 标签。
    - `_feature_importance_matrix`: 特征重要性矩阵。
    - `_full_model_alpha`: 完整模型的alpha值（正则化参数）。
    - `_max_index`: 最大百分比的索引。
    - `_max_percentage`: 最大百分比值。
    - `_is_fitted`: 布尔标志，指示模型是否已经拟合。
    - `_optimal_computed`: 布尔标志，指示是否已计算最优模型。
    - `trade_off`: 权衡参数，用于在特征数量与模型精度之间做出权衡。
    - `val_ratio`: 验证集比例，用于从训练数据中划分验证集。
    - `recompute_alpha`: 布尔值，指定是否在最优模型训练中重新计算alpha值。
    - `verbose`: 布尔值，控制日志输出的详细程度。
    - `multilabel_type`: 在多标签分类情况下特征排名的类型（默认为`"max"`）。
    ### 方法
    - `fit`: 拟合`DetachMatrix`模型，自动选择最优特征集。
    - `fit_trade_off`: 使用给定的权衡参数拟合模型。
    - `predict`: 使用已拟合的模型进行预测。
    - `score`: 获取模型的准确率得分。

    """

    def __init__(self,
                 trade_off=0.1,
                 recompute_alpha=True,
                 val_ratio=0.33,
                 verbose=False,
                 multilabel_type='max'):

        self._sfd_curve = None
        self._scaler = None
        self._classifier = None
        self._acc_train = None
        self._full_classifier = None
        self._percentage_vector = None
        self._feature_matrix = None
        self._labels = None
        self._feature_importance_matrix = None
        self._full_model_alpha = None
        self._max_index = None
        self._max_percentage = None
        self._is_fitted = False
        self._optimal_computed = False

        self.trade_off = trade_off
        self.val_ratio = val_ratio
        self.recompute_alpha = recompute_alpha
        self.verbose = verbose
        self.multilabel_type = multilabel_type

        self._full_classifier = RidgeClassifierCV(
            alphas=np.logspace(-10, 10, 20))
        self._scaler = StandardScaler(with_mean=True)

        return

    def fit(self,
            X,
            y=None,
            val_set=None,
            val_set_y=None,
            X_test=None,
            y_test=None):

        assert y is not None, "Labels are required to fit Detach Matrix"

        self._feature_matrix = X
        self._labels = y

        if val_set is not None:
            self._feature_matrix_val = val_set

        if self.verbose == True:
            print('Fitting Full Model')

        # scale feature matrix
        self._feature_matrix = self._scaler.fit_transform(self._feature_matrix)

        # Train full rocket as baseline
        self._full_classifier.fit(self._feature_matrix, y)
        self._full_model_alpha = self._full_classifier.alpha_

        print('TRAINING RESULTS Full Features:')
        print('Optimal Alpha Full Features: {:.2f}'.format(
            self._full_model_alpha))
        print('Train Accuraccy Full Features: {:.2f}%'.format(
            100 * self._full_classifier.score(self._feature_matrix, y)))
        print('-------------------------')

        # If fixed percentage is not provided, we set the number of features using the validation set
        if self.fixed_percentage is None:

            # Assert no test set is provided
            assert X_test is None, "X_test is not allowed when using trade-off, SFD curves are  computed with a validation set."

            if val_set is not None:
                X_train = self._feature_matrix
                X_val = self._feature_matrix_val
                y_train = y
                y_val = val_set_y
            else:
                # Train-Validation split
                X_train, X_val, y_train, y_val = train_test_split(
                    self._feature_matrix,
                    y,
                    test_size=self.val_ratio,
                    random_state=42,
                    stratify=y)

            # Train model for selected features
            sfd_classifier = RidgeClassifier(alpha=self._full_model_alpha)
            sfd_classifier.fit(X_train, y_train)

            # Feature Detachment
            if self.verbose == True:
                print('Applying Sequential Feature Detachment')

            self._percentage_vector, _, self._sfd_curve, self._feature_importance_matrix = feature_detachment(
                sfd_classifier,
                X_train,
                X_val,
                y_train,
                y_val,
                verbose=self.verbose,
                multilabel_type=self.multilabel_type)

            self._is_fitted = True

            # Training Optimal Model
            if self.verbose == True:
                print('Training Optimal Model')

            self.fit_trade_off(self.trade_off)

        # If fixed percentage is provided, no validation set is required
        else:
            # Assert there is no validation set
            assert val_set is None, "Validation set is not allowed when using fixed percentage of features, since it is not required for training"
            # Assert that both X_test set and y_test labels are provided
            assert X_test is not None, "X_test is required to fit Detach Matrix with fixed percentage. It is not used for training, but for plotting the feature detachment curve."
            assert y_test is not None, "y_test is required to fit Detach Matrix with fixed percentage. . It is not used for training, but for plotting the feature detachment curve."

            # We don't need to split the data into train and validation
            # We are using a fixed percentage of features
            X_train = self._feature_matrix
            y_train = y
            X_test = self._scaler.transform(
                self._full_transformer.transform(X_test))

            # Train model for selected features
            sfd_classifier = RidgeClassifier(alpha=self._full_model_alpha)
            sfd_classifier.fit(X_train, y_train)

            # Feature Detachment
            if self.verbose == True:
                print('Applying Sequential Feature Detachment')

            self._percentage_vector, _, self._sfd_curve, self._feature_importance_matrix = feature_detachment(
                sfd_classifier,
                X_train,
                X_test,
                y_train,
                y_test,
                verbose=self.verbose,
                multilabel_type=self.multilabel_type)

            self._is_fitted = True

            if self.verbose == True:
                print('Using fixed percentage of features')
            self.fit_fixed_percentage(self.fixed_percentage)

        return

    def fit_trade_off(self, trade_off=None):

        assert trade_off is not None, "Missing argument"
        assert self._is_fitted == True, "Model not fitted. Call fit method first."

        # Select optimal
        max_index, max_percentage = select_optimal_model(
            self._percentage_vector,
            self._sfd_curve,
            self._sfd_curve[0],
            self.trade_off,
            graphics=False)
        self._max_index = max_index
        self._max_percentage = max_percentage

        # Check if alpha will be recomputed
        if self.recompute_alpha:
            alpha_optimal = None
        else:
            alpha_optimal = self._full_model_alpha

        # Create feature mask
        self._feature_mask = self._feature_importance_matrix[max_index] > 0

        # Re-train optimal model
        self._classifier, self._acc_train = retrain_optimal_model(
            self._feature_mask,
            self._feature_matrix,
            self._labels,
            max_index,
            alpha_optimal,
            verbose=self.verbose)

        return

    def fit_fixed_percentage(self, fixed_percentage=None, graphics=True):

        assert fixed_percentage is not None, "Missing argument"
        assert self._is_fitted == True, "Model not fitted. Call fit method first."

        self._max_index = (np.abs(self._percentage_vector -
                                  self.fixed_percentage)).argmin()
        self._max_percentage = self._percentage_vector[self._max_index]

        # Check if alpha will be recomputed
        if self.recompute_alpha:
            alpha_optimal = None
        else:
            alpha_optimal = self._full_model_alpha

        # Create feature mask
        self._feature_mask = self._feature_importance_matrix[
            self._max_index] > 0

        # Re-train optimal model
        self._classifier, self._acc_train = retrain_optimal_model(
            self._feature_mask,
            self._feature_matrix,
            self._labels,
            self._max_index,
            alpha_optimal,
            verbose=self.verbose)

        return

    def predict(self, X):

        assert self._is_fitted == True, "Model not fitted. Call fit method first."

        # Transform time series to feature matrix
        scaled_X = self._scaler.transform(X)
        masked_scaled_X = scaled_X[:, self._feature_mask]

        y_pred = self._classifier.predict(masked_scaled_X)

        return y_pred

    def score(self, X, y):

        assert self._is_fitted == True, "Model not fitted. Call fit method first."

        # Transform time series to feature matrix
        scaled_X = self._scaler.transform(X)
        masked_scaled_X = scaled_X[:, self._feature_mask]

        return self._classifier.score(masked_scaled_X,
                                      y), self._full_classifier.score(
                                          scaled_X, y)
