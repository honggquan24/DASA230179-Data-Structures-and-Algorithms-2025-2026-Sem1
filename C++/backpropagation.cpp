#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <memory>
#include <cassert>
#include <string>

// Forward declarations
class Layer;
class NetworkNode;

// Activation functions
namespace ActivationFunction {
    double sigmoid(double x) {
        return 1.0 / (1.0 + std::exp(-x));
    }
    
    double sigmoidDerivative(double x) {
        double s = sigmoid(x);
        return s * (1.0 - s);
    }
    
    double relu(double x) {
        return std::max(0.0, x);
    }
    
    double reluDerivative(double x) {
        return x > 0 ? 1.0 : 0.0;
    }
    
    double tanh_func(double x) {
        return std::tanh(x);
    }
    
    double tanhDerivative(double x) {
        double t = std::tanh(x);
        return 1.0 - t * t;
    }
}

// Dynamic array implementation for weights and biases
template<typename T>
class DynamicArray {
private:
    T* data;
    size_t size;
    size_t capacity;

public:
    DynamicArray(size_t initial_capacity = 10) 
        : size(0), capacity(initial_capacity) {
        data = new T[capacity];
    }
    
    ~DynamicArray() {
        delete[] data;
    }
    
    // Copy constructor
    DynamicArray(const DynamicArray& other) 
        : size(other.size), capacity(other.capacity) {
        data = new T[capacity];
        for (size_t i = 0; i < size; ++i) {
            data[i] = other.data[i];
        }
    }
    
    // Assignment operator
    DynamicArray& operator=(const DynamicArray& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            capacity = other.capacity;
            data = new T[capacity];
            for (size_t i = 0; i < size; ++i) {
                data[i] = other.data[i];
            }
        }
        return *this;
    }
    
    void push_back(const T& value) {
        if (size >= capacity) {
            resize();
        }
        data[size++] = value;
    }
    
    T& operator[](size_t index) {
        assert(index < size);
        return data[index];
    }
    
    const T& operator[](size_t index) const {
        assert(index < size);
        return data[index];
    }
    
    size_t getSize() const { return size; }
    
    void clear() { size = 0; }
    
private:
    void resize() {
        capacity *= 2;
        T* newData = new T[capacity];
        for (size_t i = 0; i < size; ++i) {
            newData[i] = data[i];
        }
        delete[] data;
        data = newData;
    }
};

// Linked list node for computation graph
class ComputationNode {
public:
    double value;
    double gradient;
    DynamicArray<ComputationNode*> children;
    DynamicArray<double> childWeights;
    std::string operation;
    
    ComputationNode(double val = 0.0, const std::string& op = "input") 
        : value(val), gradient(0.0), operation(op) {}
    
    void addChild(ComputationNode* child, double weight = 1.0) {
        children.push_back(child);
        childWeights.push_back(weight);
    }
    
    void computeForward() {
        if (operation == "sum") {
            value = 0.0;
            for (size_t i = 0; i < children.getSize(); ++i) {
                value += children[i]->value * childWeights[i];
            }
        } else if (operation == "sigmoid") {
            if (children.getSize() > 0) {
                value = ActivationFunction::sigmoid(children[0]->value);
            }
        } else if (operation == "relu") {
            if (children.getSize() > 0) {
                value = ActivationFunction::relu(children[0]->value);
            }
        }
    }
    
    void computeBackward() {
        if (operation == "sum") {
            for (size_t i = 0; i < children.getSize(); ++i) {
                children[i]->gradient += gradient * childWeights[i];
            }
        } else if (operation == "sigmoid") {
            if (children.getSize() > 0) {
                children[0]->gradient += gradient * ActivationFunction::sigmoidDerivative(children[0]->value);
            }
        } else if (operation == "relu") {
            if (children.getSize() > 0) {
                children[0]->gradient += gradient * ActivationFunction::reluDerivative(children[0]->value);
            }
        }
    }
};

// Linked list for maintaining computation order
class ComputationGraph {
private:
    struct GraphNode {
        ComputationNode* compNode;
        GraphNode* next;
        
        GraphNode(ComputationNode* node) : compNode(node), next(nullptr) {}
    };
    
    GraphNode* head;
    GraphNode* tail;
    
public:
    ComputationGraph() : head(nullptr), tail(nullptr) {}
    
    ~ComputationGraph() {
        clear();
    }
    
    void addNode(ComputationNode* node) {
        GraphNode* newNode = new GraphNode(node);
        if (!head) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }
    
    void forwardPass() {
        GraphNode* current = head;
        while (current) {
            current->compNode->computeForward();
            current = current->next;
        }
    }
    
    void backwardPass() {
        // Collect nodes in reverse order for backward pass
        DynamicArray<ComputationNode*> reverseOrder;
        GraphNode* current = head;
        while (current) {
            reverseOrder.push_back(current->compNode);
            current = current->next;
        }
        
        // Execute backward pass in reverse order
        for (int i = reverseOrder.getSize() - 1; i >= 0; --i) {
            reverseOrder[i]->computeBackward();
        }
    }
    
    void clear() {
        while (head) {
            GraphNode* temp = head;
            head = head->next;
            delete temp;
        }
        tail = nullptr;
    }
    
    void resetGradients() {
        GraphNode* current = head;
        while (current) {
            current->compNode->gradient = 0.0;
            current = current->next;
        }
    }
};

// Neural Network Layer using arrays
class Layer {
private:
    size_t inputSize;
    size_t outputSize;
    DynamicArray<DynamicArray<double>> weights;  // 2D array for weights
    DynamicArray<double> biases;
    DynamicArray<double> outputs;
    DynamicArray<double> inputs;
    DynamicArray<double> weightGradients;
    DynamicArray<double> biasGradients;
    std::string activationType;

public:
    Layer(size_t in_size, size_t out_size, const std::string& activation = "sigmoid") 
        : inputSize(in_size), outputSize(out_size), activationType(activation) {
        
        // Initialize weights and biases randomly
        std::random_device rd;
        std::mt19937 gen(rd());
        std::normal_distribution<double> dist(0.0, 0.1);
        
        // Initialize weight matrix
        for (size_t i = 0; i < outputSize; ++i) {
            DynamicArray<double> row;
            for (size_t j = 0; j < inputSize; ++j) {
                row.push_back(dist(gen));
            }
            weights.push_back(row);
        }
        
        // Initialize biases
        for (size_t i = 0; i < outputSize; ++i) {
            biases.push_back(dist(gen));
        }
        
        // Initialize output arrays
        for (size_t i = 0; i < outputSize; ++i) {
            outputs.push_back(0.0);
            biasGradients.push_back(0.0);
        }
        
        // Initialize weight gradients
        for (size_t i = 0; i < outputSize * inputSize; ++i) {
            weightGradients.push_back(0.0);
        }
    }
    
    DynamicArray<double> forward(const DynamicArray<double>& input) {
        // Store input for backward pass
        inputs.clear();
        for (size_t i = 0; i < input.getSize(); ++i) {
            inputs.push_back(input[i]);
        }
        
        // Compute weighted sum + bias for each output neuron
        for (size_t i = 0; i < outputSize; ++i) {
            double sum = biases[i];
            for (size_t j = 0; j < inputSize; ++j) {
                sum += weights[i][j] * input[j];
            }
            
            // Apply activation function
            if (activationType == "sigmoid") {
                outputs[i] = ActivationFunction::sigmoid(sum);
            } else if (activationType == "relu") {
                outputs[i] = ActivationFunction::relu(sum);
            } else if (activationType == "tanh") {
                outputs[i] = ActivationFunction::tanh_func(sum);
            } else {
                outputs[i] = sum; // Linear activation
            }
        }
        
        return outputs;
    }
    
    DynamicArray<double> backward(const DynamicArray<double>& outputGradients, double learningRate = 0.01) {
        DynamicArray<double> inputGradients;
        for (size_t i = 0; i < inputSize; ++i) {
            inputGradients.push_back(0.0);
        }
        
        // Compute gradients
        for (size_t i = 0; i < outputSize; ++i) {
            double outputGrad = outputGradients[i];
            
            // Apply activation derivative
            if (activationType == "sigmoid") {
                outputGrad *= ActivationFunction::sigmoidDerivative(outputs[i]);
            } else if (activationType == "relu") {
                outputGrad *= ActivationFunction::reluDerivative(outputs[i]);
            } else if (activationType == "tanh") {
                outputGrad *= ActivationFunction::tanhDerivative(outputs[i]);
            }
            
            // Update bias gradients
            biasGradients[i] = outputGrad;
            biases[i] -= learningRate * biasGradients[i];
            
            // Update weight gradients and propagate to inputs
            for (size_t j = 0; j < inputSize; ++j) {
                double weightGrad = outputGrad * inputs[j];
                weights[i][j] -= learningRate * weightGrad;
                inputGradients[j] += outputGrad * weights[i][j];
            }
        }
        
        return inputGradients;
    }
    
    void printWeights() const {
        std::cout << "Layer weights:\n";
        for (size_t i = 0; i < outputSize; ++i) {
            for (size_t j = 0; j < inputSize; ++j) {
                std::cout << weights[i][j] << " ";
            }
            std::cout << "\n";
        }
    }
};

// Neural Network using linked list of layers
class NeuralNetwork {
private:
    struct LayerNode {
        std::unique_ptr<Layer> layer;
        LayerNode* next;
        
        LayerNode(std::unique_ptr<Layer> l) : layer(std::move(l)), next(nullptr) {}
    };
    
    LayerNode* head;
    LayerNode* tail;
    size_t layerCount;

public:
    NeuralNetwork() : head(nullptr), tail(nullptr), layerCount(0) {}
    
    ~NeuralNetwork() {
        clear();
    }
    
    void addLayer(size_t inputSize, size_t outputSize, const std::string& activation = "sigmoid") {
        auto layer = std::make_unique<Layer>(inputSize, outputSize, activation);
        LayerNode* newNode = new LayerNode(std::move(layer));
        
        if (!head) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        layerCount++;
    }
    
    DynamicArray<double> predict(const DynamicArray<double>& input) {
        DynamicArray<double> currentInput = input;
        LayerNode* current = head;
        
        while (current) {
            currentInput = current->layer->forward(currentInput);
            current = current->next;
        }
        
        return currentInput;
    }
    
    void train(const DynamicArray<double>& input, const DynamicArray<double>& target, double learningRate = 0.01) {
        // Forward pass
        DynamicArray<double> prediction = predict(input);
        
        // Compute loss gradient (mean squared error)
        DynamicArray<double> lossGradient;
        for (size_t i = 0; i < prediction.getSize(); ++i) {
            lossGradient.push_back(2.0 * (prediction[i] - target[i]) / prediction.getSize());
        }
        
        // Backward pass through layers
        DynamicArray<LayerNode*> layersReverse;
        LayerNode* current = head;
        while (current) {
            layersReverse.push_back(current);
            current = current->next;
        }
        
        DynamicArray<double> currentGradient = lossGradient;
        for (int i = layersReverse.getSize() - 1; i >= 0; --i) {
            currentGradient = layersReverse[i]->layer->backward(currentGradient, learningRate);
        }
    }
    
    double computeLoss(const DynamicArray<double>& predicted, const DynamicArray<double>& target) {
        double loss = 0.0;
        for (size_t i = 0; i < predicted.getSize(); ++i) {
            double diff = predicted[i] - target[i];
            loss += diff * diff;
        }
        return loss / predicted.getSize();
    }
    
    void printArchitecture() const {
        std::cout << "Neural Network Architecture:\n";
        LayerNode* current = head;
        int layerNum = 1;
        while (current) {
            std::cout << "Layer " << layerNum << std::endl;
            current->layer->printWeights();
            current = current->next;
            layerNum++;
        }
    }
    
private:
    void clear() {
        while (head) {
            LayerNode* temp = head;
            head = head->next;
            delete temp;
        }
        tail = nullptr;
        layerCount = 0;
    }
};

// Training data generator
class DataGenerator {
public:
    static void generateXORData(DynamicArray<DynamicArray<double>>& inputs, 
                               DynamicArray<DynamicArray<double>>& targets) {
        // XOR training data
        double xorData[4][2] = {{0, 0}, {0, 1}, {1, 0}, {1, 1}};
        double xorTargets[4] = {0, 1, 1, 0};
        
        for (int i = 0; i < 4; ++i) {
            DynamicArray<double> input;
            DynamicArray<double> target;
            
            input.push_back(xorData[i][0]);
            input.push_back(xorData[i][1]);
            target.push_back(xorTargets[i]);
            
            inputs.push_back(input);
            targets.push_back(target);
        }
    }
};

// Main demonstration
int main() {
    std::cout << "=== Advanced Backpropagation with Arrays and Linked Lists ===\n\n";
    
    // Create neural network with linked list of layers
    NeuralNetwork network;
    network.addLayer(2, 4, "sigmoid");  // Input layer: 2 -> 4
    network.addLayer(4, 3, "sigmoid");  // Hidden layer: 4 -> 3
    network.addLayer(3, 1, "sigmoid");  // Output layer: 3 -> 1
    
    std::cout << "1. Network Architecture:\n";
    network.printArchitecture();
    
    // Generate training data using arrays
    DynamicArray<DynamicArray<double>> trainInputs;
    DynamicArray<DynamicArray<double>> trainTargets;
    DataGenerator::generateXORData(trainInputs, trainTargets);
    
    std::cout << "\n2. Training XOR Problem:\n";
    
    // Training loop
    double learningRate = 0.5;
    int epochs = 10000;
    
    for (int epoch = 0; epoch < epochs; ++epoch) {
        double totalLoss = 0.0;
        
        for (size_t i = 0; i < trainInputs.getSize(); ++i) {
            network.train(trainInputs[i], trainTargets[i], learningRate);
            
            // Compute loss for monitoring
            DynamicArray<double> prediction = network.predict(trainInputs[i]);
            totalLoss += network.computeLoss(prediction, trainTargets[i]);
        }
        
        if (epoch % 100 == 0) {
            std::cout << "Epoch " << epoch << ", Loss: " << totalLoss / trainInputs.getSize() << std::endl;
        }
    }
    
    // Test the trained network
    std::cout << "\n3. Testing Results:\n";
    for (size_t i = 0; i < trainInputs.getSize(); ++i) {
        DynamicArray<double> prediction = network.predict(trainInputs[i]);
        std::cout << "Input: [" << trainInputs[i][0] << ", " << trainInputs[i][1] 
                  << "] -> Predicted: " << prediction[0] 
                  << ", Target: " << trainTargets[i][0] << std::endl;
    }
    
    // Demonstrate computation graph with linked list
    std::cout << "\n4. Computation Graph Demo:\n";
    ComputationGraph graph;
    
    // Create computation nodes
    ComputationNode input1(1.0, "input");
    ComputationNode input2(0.5, "input");
    ComputationNode sum(0.0, "sum");
    ComputationNode output(0.0, "sigmoid");
    
    // Build computation graph
    sum.addChild(&input1, 0.8);
    sum.addChild(&input2, -0.3);
    output.addChild(&sum);
    
    graph.addNode(&sum);
    graph.addNode(&output);
    
    // Forward pass
    graph.forwardPass();
    std::cout << "Forward pass result: " << output.value << std::endl;
    
    // Backward pass
    output.gradient = 1.0;  // Start backprop
    graph.backwardPass();
    
    std::cout << "Gradients after backprop:\n";
    std::cout << "Input1 gradient: " << input1.gradient << std::endl;
    std::cout << "Input2 gradient: " << input2.gradient << std::endl;
    std::cout << "Sum gradient: " << sum.gradient << std::endl;
    
    std::cout << "\n=== Program completed successfully! ===\n";
    std::cin.get();
    return 0;
}